clear;


img_path=textread('../path.txt','%s');
for img_idx=1:size(img_path,1)
    tic
    I=im2double(imread(['../data/',img_path{img_idx}]));
    [H,W,~]=size(I);
    if(H/W>720/960)
        I=imresize(I,[round(H/W*960),960]);
        [H,W,~]=size(I);
        I=I((H-720)/2+1:end-(H-720)/2-1,:,:);
        H=720;
        imwrite(I,['../data/',img_path{img_idx}]);
    else
        I=imresize(I,[720,round(720*W/H)]);
        [H,W,~]=size(I);
        I=I(:,(W-960)/2+1:end-(W-960)/2,:);
        W=960;
        imwrite(I,['../data/',img_path{img_idx}]);
    end
    WIN=round(sqrt(H*W)/50);
    I= imfilter(I, fspecial('gaussian', [round(WIN/2),round(WIN/2)],10), 'replicate');
    
    seedx=round(WIN/2):WIN:H;
    seedy=round(WIN/2):WIN:W;
    [seedx,seedy]=meshgrid(seedx,seedy);
    seedx=round(seedx+WIN*rand(size(seedx))-WIN/2);
    seedy=round(seedy+WIN*rand(size(seedy))-WIN/2);
    seedx(seedx<1)=1;seedx(seedx>H)=H;
    seedy(seedy<1)=1;seedy(seedy>W)=W;
    SEED=numel(seedx);
    
    I_weight=zeros(H,W);
    I_label=ones(H,W).*SEED;
    
    for idx=1:SEED
        sx=seedx(idx);
        sy=seedy(idx);
        bx=max(sx-WIN,1);
        ex=min(sx+WIN,H);
        by=max(sy-WIN,1);
        ey=min(sy+WIN,W);
        dx=bx:ex;
        dy=by:ey;
        
        C=sum((I(dx,dy,:)-I(sx,sy,:)).^2,3);
        dC=exp(-(C));
        [ddy,ddx]=meshgrid(dy,dx);
        dD=1./sqrt((ddx-sx).^2+(ddy-sy).^2);
        dW=dC+3*dD;
        sdW=I_weight(dx,dy);
        
        tdW=sdW;
        tdW(sdW<dW)=dW(sdW<dW);
        tdL=I_label(dx,dy);
        tdL(sdW<dW)=idx;
        
        I_weight(dx,dy)=tdW;
        I_label(dx,dy)=tdL;
    end
    IR=I(:,:,1);
    IG=I(:,:,2);
    IB=I(:,:,3);
    
    chC=abs(rand(SEED,3))./5;
    mR=arrayfun(@(i)IR(seedx(i),seedy(i)).*(1+chC(i,1)),1:SEED);
    mG=arrayfun(@(i)IG(seedx(i),seedy(i)).*(1+chC(i,2)),1:SEED);
    mB=arrayfun(@(i)IB(seedx(i),seedy(i)).*(1+chC(i,3)),1:SEED);
    
    bmR=mean(mR);
    bmG=mean(mG);
    bmB=mean(mB);
    
    for x=1:H
        for y=1:W
            IR(x,y)=mR(I_label(x,y));
            IB(x,y)=mB(I_label(x,y));
            IG(x,y)=mG(I_label(x,y));
        end
    end
    SE=strel('square',floor(sqrt(WIN)/2));
    label_edge=imdilate(bwmorph(edge(I_label,1e-5),'bridge'),SE);
    IR(label_edge)=bmR*1.3;
    IG(label_edge)=bmG*1.3;
    IB(label_edge)=bmB*1.3;
    II(:,:,1)=IR;
    II(:,:,2)=IG;
    II(:,:,3)=IB;
    imwrite(uint8(II.*255),['../data/mos_',img_path{img_idx}(1:end-3),'png']);
    fid=fopen(['../data/lab_',img_path{img_idx}(1:end-3),'txt'],'wt');
    for i=1:H
        for j=1:W
            if j==W
                fprintf(fid,'%g\n',I_label(i,j));
            else
                fprintf(fid,'%g\t',I_label(i,j));
            end
        end
    end
    fclose(fid);
    
    fid=fopen(['../data/edge_',img_path{img_idx}(1:end-3),'txt'],'wt');
    for i=1:H
        for j=1:W
            if j==W
                fprintf(fid,'%g\n',label_edge(i,j));
            else
                fprintf(fid,'%g\t',label_edge(i,j));
            end
        end
    end
    fclose(fid);
    toc
    clearvars -except img_path img_idx
    disp(img_idx)
end

